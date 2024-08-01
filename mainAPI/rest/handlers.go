package rest

import (
	"fmt"
	"mainAPI/prompts"
	"net/http"

	gin "github.com/gin-gonic/gin"
)

type Message struct {
	Message string `json:"message"`
}

func GetRootHandler(c *gin.Context, app_name, API_DESCRIPTION string) {
	c.Writer.WriteHeader(http.StatusOK)
	fmt.Fprintf(c.Writer, "%s\n", app_name)
	fmt.Fprintf(c.Writer, "%s\n", API_DESCRIPTION)
}

func GetHealthHandler(c *gin.Context) {
	c.Writer.WriteHeader(http.StatusOK)
}

func PostChatHandler(c *gin.Context) {
	var message Message
	if err := c.ShouldBindJSON(&message); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
	}

	prompter, ok := c.Get(PROMPTER_NAME)
	if !ok {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "prompter not found"})
	}

	response, err := prompter.(*prompts.Prompter).PerformRAG(message.Message)

	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
	}

	c.JSON(http.StatusOK, gin.H{"response": response})

}
