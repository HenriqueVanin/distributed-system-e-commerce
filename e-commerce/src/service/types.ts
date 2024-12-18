// Produto
export interface Product {
    id: string;
    name: string;
    price: number;
    imgSrc: string;
    quantity: number;
  }
  
  // Pedido (Request)
  export interface Request {
    request_id: string;
    products: string[]; // IDs dos produtos
    status: string;
    client_id: string;
    total: number;
  }
  