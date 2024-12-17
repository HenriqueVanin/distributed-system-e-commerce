import { create } from 'zustand';

export interface ProductProps {
    id: string;
    title: string;
    imgSrc: string;
    price: string;
    quantity: number;
}

// Definindo a interface do estado e das ações
interface ProductState {
  productsAtCart: ProductProps[];
  addProductIntoCart: (product: ProductProps) => void;
  clearCart: () => void;
  removeProductFromCart: (product: ProductProps) => void;
  handleQuantityChange: (product: ProductProps, newQuantity: number) => void;
}

// Criando o store com tipos em TypeScript
const useProductStore = create<ProductState>((set) => ({
    productsAtCart: [],
    clearCart: () => set({ productsAtCart: [] }),
  
    addProductIntoCart: (product: ProductProps) =>
        set((state) => ({
          productsAtCart: state.productsAtCart.map((p) =>
            p.id === product.id ? { ...p, quantity: p.quantity + 1 } : p
          ).concat(state.productsAtCart.some((p) => p.id === product.id) ? [] : { ...product, quantity: 1 })
        })),
      
    
      removeProductFromCart: (product: ProductProps) =>
        set((state) => ({
          productsAtCart: state.productsAtCart.filter((item) => item.id !== product.id) // Remove o item específico
        })),
        handleQuantityChange: (product:ProductProps, newQuantity: number) =>
            set((state) => ({
              productsAtCart: state.productsAtCart.map((p) =>
                p.id === product.id ? { ...p, quantity: newQuantity } : p
              ),
            })),
    
}));

export default useProductStore;
