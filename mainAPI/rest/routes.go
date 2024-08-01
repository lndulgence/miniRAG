package rest

import (
	"mainAPI/prompts"

	gin "github.com/gin-gonic/gin"
)

const PROMPTER_NAME = "prompter"

func NewRouter(p *prompts.Prompter) *gin.Engine {
	gin.SetMode(gin.ReleaseMode)
	app_name := "miniRAG"
	API_DESCRIPTION := `API:
		GET / -> returns this message
		GET /health -> Kubernetes health check. Returns 200 if healthy.
		POST /chat -> receives aa user message and returns a response. Accepts a JSON object with a "message" field.
		`
	r := gin.Default()

	r.Use(func(ctx *gin.Context) {
		ctx.Set(PROMPTER_NAME, p)
		ctx.Next()
	})

	r.GET("/", func(c *gin.Context) {
		GetRootHandler(c, app_name, API_DESCRIPTION)
	})
	r.GET("/health", GetHealthHandler)
	r.POST("/chat", PostChatHandler)

	return r
}
