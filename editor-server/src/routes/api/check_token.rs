use crate::global;

use crate::db::types::user::UserData;

use axum::{http::StatusCode, response::Json};
use axum_extra::extract::CookieJar;
use redis::AsyncCommands;
use serde::{Deserialize, Serialize};

#[derive(Debug, Deserialize, Serialize)]
pub struct CheckTokenResponse {
    token: String,
}

#[derive(Debug, Deserialize, Serialize)]
pub struct CheckTokenFailedResponse {
    err: String,
}

/// Logout handler.
/// Remove token from redis and return success message.
/// Otherwise return an error message.
pub async fn check_token(
    cookie_jar: Option<CookieJar>,
) -> Result<(StatusCode, Json<CheckTokenResponse>), (StatusCode, Json<CheckTokenFailedResponse>)> {
    // Get token from cookie jar
    let cookie_jar = match cookie_jar {
        Some(cookie_jar) => cookie_jar,
        None => {
            return Err((
                StatusCode::INTERNAL_SERVER_ERROR,
                Json(CheckTokenFailedResponse {
                    err: "Failed to retrieve cookies.".to_string(),
                }),
            ))
        }
    };

    let token = match cookie_jar.get("token") {
        Some(token) => token.value().to_string(),
        None => {
            return Err((
                StatusCode::BAD_REQUEST,
                Json(CheckTokenFailedResponse {
                    err: "Token is required.".to_string(),
                }),
            ))
        }
    };
    let env_type = &global::envs::get().env;

    if env_type == "development" {
        return Ok((StatusCode::OK, Json(CheckTokenResponse { token })));
    }
    // Get app state
    let clients = global::clients::get();

    // Generate token and store it in redis
    let redis_client = clients.redis_client();
    let mut conn = redis_client.get_tokio_connection().await.unwrap();

    let id: String = conn.get(&token).await.map_err(|_| {
        (
            StatusCode::UNAUTHORIZED,
            Json(CheckTokenFailedResponse {
                err: "Unauthorized.".to_string(),
            }),
        )
    })?;

    let mysql_pool = clients.mysql_pool();

    let _ = sqlx::query_as!(
        UserData,
        r#"
            SELECT * FROM User WHERE id = ? LIMIT 1;
        "#,
        id,
    )
    .fetch_one(mysql_pool)
    .await
    .map_err(|_| {
        (
            StatusCode::NOT_FOUND,
            Json(CheckTokenFailedResponse {
                err: "User not found.".to_string(),
            }),
        )
    })?;

    Ok((StatusCode::OK, Json(CheckTokenResponse { token })))
}
