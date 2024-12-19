// Produto
export interface Product {
  id: string;
  name: string;
  price: number;
  imgSrc: string;
  quantity: number;
}

export interface Order {
  request_id: string;
  products: Product[];
  status: string;
  client_id: string;
  total: string;
  created_at: string;
}

export interface RequestPayload {
  total: string;
  client_id: string;
}
