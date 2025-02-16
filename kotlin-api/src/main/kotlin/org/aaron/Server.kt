package org.aaron

import org.http4k.core.HttpHandler
import org.http4k.core.Method.GET
import org.http4k.core.Response
import org.http4k.core.Status.Companion.OK
import org.http4k.routing.bind
import org.http4k.routing.routes
import org.http4k.server.Undertow
import org.http4k.server.asServer

fun helloWorld(): HttpHandler {
    return routes("/test" bind GET to { Response(OK).body("hello world") })
}

fun main() {
    println("begin main availableProcessors=${Runtime.getRuntime().availableProcessors()}")

    val server = helloWorld().asServer(
        Undertow(
            port = 18080,
        )
    ).start()

    println("server started port ${server.port()}")
}