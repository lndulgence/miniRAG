package prompts

import (
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"
	"strings"
	"time"
)

// Prompt is a struct that represents a prompt
type Prompt struct {
	SystemMessage string `json:"system_message"`
	UserMessage   string `json:"user_message"`
	MaxTokens     int    `json:"max_tokens"`
}

type Choice struct {
	Text string `json:"text"`
}

type Response struct {
	Choices []Choice `json:"choices"`
}

// Prompter is a struct that represents a prompter
type Prompter struct {
	SystemMessage string
	RagURL        string
	LlamaURL      string
}

// NewPrompter is a function that returns a new prompter
func NewPrompter(systemMessage string, ragURL string, llamaURL string) *Prompter {
	return &Prompter{
		SystemMessage: systemMessage,
		RagURL:        ragURL,
		LlamaURL:      llamaURL,
	}
}

func (p *Prompter) PerformRAG(usermsg string) (string, error) {
	prompt := Prompt{
		SystemMessage: p.SystemMessage,
		UserMessage:   usermsg,
		MaxTokens:     300, // Could be a parameter, but this is a demo-like app.
	}

	// Get augmented prompt
	augmentedPrompt, err := p.GetAugmentedPrompt(prompt)
	if err != nil {
		return "", fmt.Errorf("failed to get augmented prompt: %v", err)
	}

	// Get response
	response, err := p.GetResponse(augmentedPrompt)
	if err != nil {
		return "", fmt.Errorf("failed to get response: %v", err)
	}

	return response, nil

}

// Call the RAG endpoint to retrieve an augmented prompt
func (p *Prompter) GetAugmentedPrompt(prompt Prompt) (Prompt, error) {
	// Convert prompt to JSON
	promptJSON, err := json.Marshal(prompt)
	if err != nil {
		return Prompt{}, fmt.Errorf("failed to marshal prompt to JSON: %v", err)
	}

	// Send POST request to RagURL
	resp, err := http.Post(p.RagURL, "application/json", bytes.NewBuffer(promptJSON))
	if err != nil {
		return Prompt{}, fmt.Errorf("failed to send POST request to RagURL: %v", err)
	}
	defer resp.Body.Close()

	// Check response status code
	if resp.StatusCode != http.StatusOK {
		return Prompt{}, fmt.Errorf("unexpected response status code: %d", resp.StatusCode)
	}

	// Decode response body
	var augmentedPrompt Prompt
	err = json.NewDecoder(resp.Body).Decode(&augmentedPrompt)
	if err != nil {
		return Prompt{}, fmt.Errorf("failed to decode response body: %v", err)
	}

	return augmentedPrompt, nil
}

// Call the Llama endpoint to retrieve a respose to the prompt
func (p *Prompter) GetResponse(prompt Prompt) (string, error) {
	// Convert prompt to JSON
	promptJSON, err := json.Marshal(prompt)
	if err != nil {
		return "", fmt.Errorf("failed to marshal prompt to JSON: %v", err)
	}

	// Send POST request to LlamaURL

	resp, err := RetryPostRequest(p.LlamaURL, "application/json", promptJSON, 10)
	if err != nil {
		return "", fmt.Errorf("failed to send POST request to LlamaURL: %v", err)
	}
	defer resp.Body.Close()

	// Check response status code
	if resp.StatusCode != http.StatusOK {
		return "", fmt.Errorf("unexpected response status code: %d", resp.StatusCode)
	}

	// Decode response body
	var response Response
	err = json.NewDecoder(resp.Body).Decode(&response)
	if err != nil {
		return "", fmt.Errorf("failed to decode response body: %v", err)
	}

	return response.CleanUp(), nil
}

// CleanUp is a method that cleans up the response, returning only the response text.
func (r *Response) CleanUp() string {
	return strings.Split(r.Choices[0].Text, "[/INST]")[1]
}

// RetryPostRequest is a function that performs a POST request with retry and increasing backoff
// Probably not needed in production, but useful if only because im developing on a 5 year old laptop
// and the services are running on a local mononode k8s cluster, so memory and cpu are limited.
func RetryPostRequest(url string, contentType string, body []byte, maxRetries int) (*http.Response, error) {
	var resp *http.Response
	var err error

	for i := 0; i <= maxRetries; i++ {
		resp, err = http.Post(url, contentType, bytes.NewBuffer(body))
		if err == nil && resp.StatusCode == http.StatusOK {
			return resp, nil
		}

		// Calculate backoff duration
		backoff := time.Duration(i) * time.Second * 10

		// Wait for backoff duration
		time.Sleep(backoff)
	}

	return nil, fmt.Errorf("failed to perform POST request after %d retries", maxRetries)
}
