// Form field data
const formFields = [
    { id: 'nome', label: 'Nome:', placeholder: 'Nome do produto' },
    { id: 'valor', label: 'Valor:', placeholder: 'Valor do produto' },
    { id: 'quantidade', label: 'Quantidade:', placeholder: 'Quantidade em estoque' },
    { id: 'descricao', label: 'Descrição:', placeholder: 'Descrição do produto' },
    { id: 'fornecedor', label: 'Fornecedor:', placeholder: 'Nome do fornecedor' }
];

// Store products in memory (in a real application, this would be a database)
let products = [];

// Initialize event listeners when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    const actionButtons = document.querySelectorAll('.action-button');
    
    actionButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            const action = e.target.textContent.toLowerCase();
            handleAction(action);
        });
    });
});

// Handle different actions
function handleAction(action) {
    switch(action) {
        case 'adicionar':
            addProduct();
            break;
        case 'atualizar':
            updateProduct();
            break;
        case 'deletar':
            deleteProduct();
            break;
        case 'ver item':
            viewProduct();
            break;
    }
}

// Add a new product
function addProduct() {
    const product = getFormData();
    if (validateProduct(product)) {
        products.push(product);
        clearForm();
        updateTotalValue();
        alert('Produto adicionado com sucesso!');
    }
}

// Update existing product
function updateProduct() {
    const productName = document.getElementById('nome').value;
    const index = products.findIndex(p => p.nome === productName);
    
    if (index !== -1) {
        const product = getFormData();
        if (validateProduct(product)) {
            products[index] = product;
            clearForm();
            updateTotalValue();
            alert('Produto atualizado com sucesso!');
        }
    } else {
        alert('Produto não encontrado!');
    }
}

// Delete a product
function deleteProduct() {
    const productName = document.getElementById('nome').value;
    const index = products.findIndex(p => p.nome === productName);
    
    if (index !== -1) {
        products.splice(index, 1);
        clearForm();
        updateTotalValue();
        alert('Produto deletado com sucesso!');
    } else {
        alert('Produto não encontrado!');
    }
}

// View product details
function viewProduct() {
    const productName = document.getElementById('nome').value;
    const product = products.find(p => p.nome === productName);
    
    if (product) {
        Object.keys(product).forEach(key => {
            const input = document.getElementById(key);
            if (input) {
                input.value = product[key];
            }
        });
    } else {
        alert('Produto não encontrado!');
    }
}

// Get form data
function getFormData() {
    const product = {};
    formFields.forEach(field => {
        product[field.id] = document.getElementById(field.id).value;
    });
    return product;
}

// Validate product data
function validateProduct(product) {
    for (const key in product) {
        if (!product[key]) {
            alert(`Por favor, preencha o campo ${key}`);
            return false;
        }
    }
    return true;
}

// Clear form fields
function clearForm() {
    formFields.forEach(field => {
        document.getElementById(field.id).value = '';
    });
}

// Update total value display
function updateTotalValue() {
    const total = products.reduce((sum, product) => {
        const value = parseFloat(product.valor) || 0;
        const quantity = parseInt(product.quantidade) || 0;
        return sum + (value * quantity);
    }, 0);
    
    const totalCard = document.querySelector('.total-card h2');
    totalCard.textContent = `Valor Total dos Itens: R$ ${total.toFixed(2)}`;
}