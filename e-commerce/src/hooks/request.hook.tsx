import {
  createRequest,
  listRequests,
  removeRequest,
  updatePayment,
} from "../service/requestService";
import { Order } from "../service/types";
import useProductStore from "../store/product.store";
import { useToast } from "./toast.hook";

export const useRequest = () => {
  const { setOrders } = useProductStore();

  const { triggerToast } = useToast();
  const updateOrders = async () => {
    const res = await listRequests();
    if (res) setOrders(res);
  };

  const removeOrder = async (request: Order) => {
    await removeRequest(request.request_id);
    triggerToast("Pedido removido com sucesso");
    updateOrders();
  };

  const createOrder = async (request: Order) => {
    await createRequest(request);
    triggerToast("Pedido criado com sucesso");
    updateOrders();
  };

  const updatePaymentAction = async (request: Order, status: string) => {
    await updatePayment(request, status);
    triggerToast("Pagamento atualizado com sucesso");
    updateOrders();
  };

  return { removeOrder, updateOrders, createOrder, updatePaymentAction };
};
