FROM golang:1.18-alpine
RUN apk update

COPY rest /app/rest
COPY go.mod /app/
COPY go.sum /app/
COPY main.go /app/
COPY args.go /app/
COPY prompts /app/prompts
RUN ls /app
WORKDIR /app
RUN go build -o mainAPI
