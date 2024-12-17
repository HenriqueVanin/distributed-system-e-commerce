import { Bounce, toast } from "react-toastify";

export const useToast = () => {
    const triggerToast = (message: string) => {
        toast(message, {
            position: "bottom-center",
            autoClose: 1000,
            hideProgressBar: false,
            closeOnClick: true,
            pauseOnHover: true,
            draggable: true,
            progress: undefined,
            theme: "dark",
            transition: Bounce,
            });
    }
    return {
        triggerToast
    };
};