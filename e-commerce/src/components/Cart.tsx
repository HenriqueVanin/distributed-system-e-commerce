import React from "react";
import useProductStore, { ProductProps } from "../store/product.store";


const Cart: React.FC = () => {
  const {productsAtCart, removeProductFromCart} = useProductStore()

  // const handleQuantityChange = (id: number, quantity: number) => {
  //   setCart((prevCart) =>
  //     prevCart.map((item) =>
  //       item.id === id ? { ...item, quantity: Math.max(1, quantity) } : item
  //     )
  //   );
  // };

  const handleRemoveItem = (product: ProductProps) => {
    removeProductFromCart(product)
  };

  const calculateTotal = () => {
    return productsAtCart
    .map((item) => Number(item.price)) // Converte 'price' para string e depois para número
    .reduce((sum, price) => sum + price, 0); // Soma os valores
};


  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Shopping Cart</h1>

      <div className="flex gap-4">
        {productsAtCart.map((product: ProductProps) => (
          <div
            key={product.id}
            className="card bg-base-100 shadow-md p-4 flex justify-between items-center"
          >
            <div className="flex">
              <h2 className="text-lg font-semibold">{product.title}</h2>
              <p className="text-sm text-gray-500">${product.price}</p>
            </div>
            <div className="flex items-center gap-2">
              <input
                type="number"
                min="1"
                value={product.quantity}
                onChange={(e) =>
                  handleQuantityChange(product.id, parseInt(e.target.value))
                }
                className="input input-bordered w-16 text-center"
              />
              <button
                onClick={() => handleRemoveItem(product)}
                className="btn btn-error btn-sm"
              >
                Remove
              </button>
            </div>
          </div>
        ))}
      </div>

      <div className="mt-6">
        <h2 className="text-xl font-semibold">Total: ${calculateTotal()}</h2>
        <button className="btn btn-primary mt-4">Checkout</button>
      </div>
    </div>
  );
};

export default Cart;
