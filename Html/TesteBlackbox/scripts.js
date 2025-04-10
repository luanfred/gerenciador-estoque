// Sistema de Autenticação
const auth = {
    login: () => localStorage.setItem('isAuthenticated', 'true'),
    logout: () => localStorage.removeItem('isAuthenticated'),
    checkAuth: () => localStorage.getItem('isAuthenticated') === 'true'
};

// Gerenciamento de Produtos
const productManager = {
    getProducts: () => JSON.parse(localStorage.getItem('products') || '[]'),
    saveProduct: (product) => {
        const products = productManager.getProducts();
        products.push(product);
        localStorage.setItem('products', JSON.stringify(products));
    },
    calculateTotal: () => {
        return productManager.getProducts().reduce((total, product) => {
            return total + (product.valor * product.quantidade);
        }, 0);
    }
};

// Controle de Navegação
const navigateTo = (page) => {
    if (page === 'login') auth.logout();
    window.location.href = `${page}.html`;
};

// Login
document.getElementById('loginForm')?.addEventListener('submit', (e) => {
    e.preventDefault();
    auth.login();
    navigateTo('inventario');
});

// Inventário
if (window.location.pathname.includes('inventario')) {
    if (!auth.checkAuth()) navigateTo('index');
    
    const renderTable = () => {
        const tbody = document.getElementById('tabelaCorpo');
        tbody.innerHTML = productManager.getProducts().map(product => `
            <tr>
                <td>${product.nome}</td>
                <td>R$ ${product.valor.toFixed(2)}</td>
                <td>${product.quantidade}</td>
                <td>${product.descricao}</td>
                <td>${product.fornecedor}</td>
            </tr>
        `).join('');
    };
    
    document.getElementById('btnCadastro').addEventListener('click', () => navigateTo('cadastro'));
    document.getElementById('btnLogout').addEventListener('click', () => navigateTo('index'));
    renderTable();
}

// Cadastro de Produtos
if (window.location.pathname.includes('cadastro')) {
    if (!auth.checkAuth()) navigateTo('index');
    
    const form = document.getElementById('productForm');
    const updateTotal = () => {
        document.getElementById('totalValue').textContent = 
            `R$ ${productManager.calculateTotal().toFixed(2)}`;
    };
    
    document.getElementById('btnAdicionar').addEventListener('click', () => {
        const product = {
            nome: document.getElementById('nome').value,
            valor: parseFloat(document.getElementById('valor').value),
            quantidade: parseInt(document.getElementById('quantidade').value),
            descricao: document.getElementById('descricao').value,
            fornecedor: document.getElementById('fornecedor').value
        };
        
        productManager.saveProduct(product);
        form.reset();
        updateTotal();
    });
    
    document.getElementById('btnLimpar').addEventListener('click', () => form.reset());
    updateTotal();
}