import {
  createProduct,
  fetchStock,
  listProducts,
  removeProduct,
  updateProduct,
} from "../service/productService";
import { Product } from "../service/types";
import useProductStore from "../store/product.store";

export const useProduct = () => {
  const { productsAtCart, setStorageProducts, setProductsAtCart } =
    useProductStore();
  const calculateTotalQuantity = (): number => {
    return productsAtCart
      .map((item) => Number(item.quantity)) // Converte 'price' para string e depois para número
      .reduce((sum, quantity) => sum + quantity, 0); // Soma os totales
  };
  const calculateTotalPrice = (): number => {
    console.log(productsAtCart);
    return productsAtCart
      .map((item) => Number(item.price) * item.quantity) // Converte 'price' para string e depois para número
      .reduce((sum, price) => sum + price, 0); // Soma os totales
  };
  const updateShop = async () => {
    const res = await fetchStock();
    if (res) setStorageProducts(res);
  };

  const getCart = async () => {
    const res = await listProducts();
    if (res) setProductsAtCart(res);
  };

  const addProductIntoCart = async (product: Product) => {
    if (productsAtCart.some((p) => p.id === product.id)) {
      const actualQuantity = productsAtCart.find(
        (p) => p.id === product.id
      )?.quantity;
      await updateProductAtCart({
        ...product,
        quantity: (actualQuantity ?? 1) + 1,
      });
    } else {
      await createProduct(product);
    }
    getCart();
  };

  const updateProductAtCart = async (product: Product) => {
    await updateProduct(product.id, product);
    getCart();
  };

  const removeProductFromCart = async (product: Product) => {
    await removeProduct(product.id);
    getCart();
  };

  return {
    calculateTotalQuantity,
    addProductIntoCart,
    updateShop,
    getCart,
    calculateTotalPrice,
    updateProductAtCart,
    removeProductFromCart,
  };
};
