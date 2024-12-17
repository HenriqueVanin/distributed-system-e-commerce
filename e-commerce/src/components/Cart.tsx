import React, { useState } from "react";

// Item interface
interface CartItem {
  id: number;
  name: string;
  price: number;
  quantity: number;
}

const Cart: React.FC = () => {
  const [cart, setCart] = useState<CartItem[]>([
    { id: 1, name: "Product A", price: 25.0, quantity: 1 },
    { id: 2, name: "Product B", price: 15.0, quantity: 2 },
  ]);

  const handleQuantityChange = (id: number, quantity: number) => {
    setCart((prevCart) =>
      prevCart.map((item) =>
        item.id === id ? { ...item, quantity: Math.max(1, quantity) } : item
      )
    );
  };

  const handleRemoveItem = (id: number) => {
    setCart((prevCart) => prevCart.filter((item) => item.id !== id));
  };

  const calculateTotal = () => {
    return cart
      .reduce((total, item) => total + item.price * item.quantity, 0)
      .toFixed(2);
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Shopping Cart</h1>

      <div className="flex gap-4">
        {cart.map((item) => (
          <div
            key={item.id}
            className="card bg-base-100 shadow-md p-4 flex justify-between items-center"
          >
            <div className="flex">
              <h2 className="text-lg font-semibold">{item.name}</h2>
              <p className="text-sm text-gray-500">${item.price.toFixed(2)}</p>
            </div>
            <div className="flex items-center gap-2">
              <input
                type="number"
                min="1"
                value={item.quantity}
                onChange={(e) =>
                  handleQuantityChange(item.id, parseInt(e.target.value))
                }
                className="input input-bordered w-16 text-center"
              />
              <button
                onClick={() => handleRemoveItem(item.id)}
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
