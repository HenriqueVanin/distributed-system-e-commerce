import qrCode from "../assets/qr-code.jpg";
import { useProduct } from "../hooks/product.hook";

export const Checkout = () => {
  const { calculateTotalPrice } = useProduct();
  return (
    <div className="flex justify-center items-center h-full">
      <div className="flex items-center justify-center">
        <div className="flex-col w-[200px] flex-grow mx-auto items-end p-4 gap-3">
          <p>Total:</p>
          <p className="text-secondary text-[40px] font-bold">
            Ȼ {calculateTotalPrice()}
          </p>
        </div>
        <div className="flex-col flex-grow mx-auto p-4 gap-3">
          <div className="grid w-[300px] flex-grow mx-auto p-4 gap-3">
            <input
              type="email"
              placeholder="Email"
              className="input input-bordered w-full"
            />
            <input
              type="password"
              placeholder="Password"
              className="input input-bordered w-full"
            />
            <div className="flex justify-center text-sm">
              <p>Use the QR code below to pay</p>
            </div>
            <div className="bg-white p-12">
              <img src={qrCode} alt="QR Code" />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
