use axum::{headers::HeaderMap, http::StatusCode, response::Json};

use serde::{Deserialize, Serialize};

#[derive(Debug, Deserialize, Serialize)]
pub struct LoginQuery {
    username: String,
    password: String,
}

#[derive(Debug, Deserialize, Serialize)]
pub struct LoginResponse {
    token: String,
}

#[derive(Debug, Deserialize, Serialize)]
pub struct LoginFailedResponse {
    err: String,
}

/// Login handler.
/// Return a token in cookie if login is successful.
/// Otherwise return an error message.
pub async fn login(
    _query: Option<Json<LoginQuery>>,
) -> Result<(StatusCode, (HeaderMap, Json<LoginResponse>)), (StatusCode, Json<LoginFailedResponse>)>
{
    todo!()
}
