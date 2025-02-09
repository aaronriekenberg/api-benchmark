package main

import (
	"bytes"
	"fmt"
	"io"
	"log/slog"
	"net/http"
	"os"
	"runtime"
	"runtime/debug"
	"strings"
)

func healthHandlerFunc() http.HandlerFunc {
	const responseBodyString = "hello world"

	responseBodyBytes := []byte(responseBodyString)

	return func(w http.ResponseWriter, r *http.Request) {

		io.Copy(w, bytes.NewReader(responseBodyBytes))
	}
}

func runHTTPServer() {
	const addr = ":18080"

	mux := http.NewServeMux()

	mux.Handle("GET /test", healthHandlerFunc())

	slog.Info("starting server",
		"addr", addr,
	)

	server := http.Server{
		Handler: mux,
		Addr:    addr,
	}
	server.ListenAndServe()
}

func main() {
	defer func() {
		if err := recover(); err != nil {
			slog.Error("panic in main",
				"error", err,
			)
			fmt.Fprintf(os.Stderr, "stack trace:\n%v", string(debug.Stack()))
			os.Exit(1)
		}
	}()

	setupSlog()

	slog.Info("begin main",
		"GOMAXPROCS", runtime.GOMAXPROCS(-1),
		"buildInfoMap", buildInfoMap(),
		"goEnvironVariables", goEnvironVariables(),
	)

	runHTTPServer()
}

func setupSlog() {
	level := slog.LevelInfo

	if levelString, ok := os.LookupEnv("LOG_LEVEL"); ok {
		err := level.UnmarshalText([]byte(levelString))
		if err != nil {
			panic(fmt.Errorf("level.UnmarshalText error %w", err))
		}
	}

	slog.SetDefault(
		slog.New(
			slog.NewJSONHandler(
				os.Stdout,
				&slog.HandlerOptions{
					Level: level,
				},
			),
		),
	)

	slog.Info("setupSlog",
		"configuredLevel", level,
	)
}

func buildInfoMap() map[string]string {
	buildInfoMap := make(map[string]string)

	if buildInfo, ok := debug.ReadBuildInfo(); ok {
		buildInfoMap["GoVersion"] = buildInfo.GoVersion
		for _, setting := range buildInfo.Settings {
			if strings.HasPrefix(setting.Key, "GO") ||
				strings.HasPrefix(setting.Key, "vcs") {
				buildInfoMap[setting.Key] = setting.Value
			}
		}
	}

	return buildInfoMap
}

func goEnvironVariables() []string {
	var goVars []string
	for _, env := range os.Environ() {
		if strings.HasPrefix(env, "GO") {
			goVars = append(goVars, env)
		}
	}
	return goVars
}
