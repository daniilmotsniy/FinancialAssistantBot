docker build --rm -t financial_assistant .
docker run -p 3000:3000 --pid=host financial_assistant