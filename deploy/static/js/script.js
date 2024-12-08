// Function to create and display chat bubbles
function appendMessage(message, type) {
    const chatBox = document.getElementById('chatBox');

    const messageElement = document.createElement('div');
    messageElement.classList.add('message');
    messageElement.classList.add(type); // user-message or bot-message
    messageElement.innerText = message;

    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight; // Scroll to the latest message
}

// Function to send the user input to the FastAPI backend and receive similar abstracts
async function sendQuery() {
    const query = document.getElementById('queryInput').value;

    if (!query) {
        alert("Please enter a query.");
        return;
    }

    // Display user message
    appendMessage(query, 'user-message');

    // Show loading message from bot
    appendMessage("Searching for similar abstracts...", 'bot-message');

    try {
        // Send POST request to FastAPI API
        const response = await fetch('http://127.0.0.1:8000/find_similar_abstracts/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: query })
        });

        const data = await response.json();

        if (response.ok) {
            // Clear results message
            const mostSimilarAbstract = data.most_similar_abstract;
            const similarityScore = data.similarity_score;
            const title = data.title;
            const authors = data.authors;

            // Display bot response with title, authors, similarity score, and abstract
            appendMessage(`Here is the most similar abstract:\n\nTitle: ${title}\nAuthors: ${authors}\n\nSimilarity Score: ${similarityScore}\n\n${mostSimilarAbstract}`, 'bot-message');
        } else {
            appendMessage(`Error: ${data.detail}`, 'bot-message');
        }
    } catch (error) {
        console.error(error);
        appendMessage("Error: Could not fetch data from the server.", 'bot-message');
    }
}
