//input: gets a single object json
//output: designing it and prints on the page 
function createResultCard(item) {
    const card = document.createElement('div');
    card.className = 'result-card';
    card.innerHTML = `
        <h3>File: ${item.file_letter}</h3>
        <p><strong>Paragraph:</strong> ${item.paragraph_marker}</p>
        <p><strong>Page:</strong> ${item.page}</p>
        <p><strong>Word:</strong> ${item.word}</p>
        <p><strong>Sentence:</strong> ${item.sentence}</p>
    `;
    return card;
}

window.searchWord = async function() {
    const word = document.getElementById('wordInput').value;
    const resultDiv = document.getElementById('result');
    resultDiv.innerHTML = '<p class="loading">Searching...</p>';
    
    try {
        const response = await fetch(`/api/PersonalPage/${encodeURIComponent(word)}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        if (!response.ok) {
            throw new Error(`Server responded with status ${response.status}`);
        }
        
        const stringData = await response.json(); // thats string because we got out output in "stdout" form.
        const jsonData = JSON.parse(stringData);
        
        resultDiv.innerHTML = '';
        
        if (Array.isArray(jsonData)) {
            jsonData.forEach(item => {
                resultDiv.appendChild(createResultCard(item));
            });
        } else {
            // Handle single item
            resultDiv.appendChild(createResultCard(jsonData));
        }
    } catch (error) {
        console.error('Search error:', error);
        resultDiv.innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
    }
};