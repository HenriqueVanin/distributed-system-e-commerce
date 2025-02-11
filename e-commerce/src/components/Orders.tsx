import useProductStore from "../store/product.store";
import { Order } from "../service/types";
import { useEffect } from "react";
import { useRequest } from "../hooks/request.hook";

const Orders: React.FC = () => {
  const { updateOrders, removeOrder, updatePaymentAction } = useRequest();
  const { orders } = useProductStore();
  useEffect(() => {
    updateOrders();
  }, []);

  return (
    <div className="grid w-[900px] flex-grow mx-auto p-4">
      <div className="grid gap-4 flex-grow h-full items-start">
        {orders.map((order: Order) => (
          <div
            key={order.request_id}
            className="w-full bg-base-100 shadow-md p-4 flex justify-between items-center"
          >
            <div className="flex w-full items-center justify-between gap-2">
              <div className="flex gap-2">
                <h2 className="text-lg font-semibold">{order.request_id}</h2>
                <h2 className="text-lg font-semibold">
                  {order.status?.toLocaleUpperCase()}
                </h2>
              </div>

              <div className="grid">
                <h2 className="text-xs font-semibold">
                  {new Date(order.created_at).toDateString()}
                </h2>
              </div>
              <div className="flex items-center gap-2">
                <p
                  className="w-12
                 justify-end flex text-lg text-secondary font-semibold"
                >
                  ${order.total}
                </p>
                <button
                  onClick={() => removeOrder(order)}
                  className="btn btn-error btn-sm"
                >
                  Remove
                </button>
                {order.status === "criado" && (
                  <>
                    <button
                      onClick={() => updatePaymentAction(order, "aprovado")}
                      className="btn btn-success btn-sm"
                    >
                      Aprove
                    </button>{" "}
                    <button
                      onClick={() => updatePaymentAction(order, "recusado")}
                      className="btn btn-warning btn-sm"
                    >
                      Reprove
                    </button>
                  </>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Orders;
