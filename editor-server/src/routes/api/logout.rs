use axum::{http::StatusCode, response::Json};
use axum_extra::extract::CookieJar;

use serde::{Deserialize, Serialize};

#[derive(Debug, Deserialize, Serialize)]
pub struct LogoutResponse {
    success: bool,
}

#[derive(Debug, Deserialize, Serialize)]
pub struct LogoutFailedResponse {
    err: String,
}

/// Logout handler.
/// Remove token from redis and return success message.
/// Otherwise return an error message.
pub async fn logout(
    _cookie_jar: Option<CookieJar>,
) -> Result<(StatusCode, Json<LogoutResponse>), (StatusCode, Json<LogoutFailedResponse>)> {
    todo!()
}
