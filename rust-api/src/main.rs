use axum::{Router, routing::get};

#[tokio::main]
async fn main() {
    // build our application with a route
    let app = Router::new().route("/test", get(handler));

    // run it
    let listener = tokio::net::TcpListener::bind("127.0.0.1:8080")
        .await
        .unwrap();
    println!("listening on {}", listener.local_addr().unwrap());
    axum::serve(listener, app).await.unwrap();
}

async fn handler() -> &'static str {
    "hello world"
}
