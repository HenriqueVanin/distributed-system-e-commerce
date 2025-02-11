import { useEffect, useState } from "react";
import { MdNotifications } from "react-icons/md";

const Messenger: React.FC = () => {
  const [messages, setMessages] = useState<
    {
      request_id: string;
      status: string;
      client_id: string;
      total: string;
      created_at: string;
    }[]
  >([]);

  useEffect(() => {
    // Conecta ao servidor Flask-SSE
    const eventSource = new EventSource("http://127.0.0.1:5000/stream");
    console.log(eventSource);
    eventSource.onopen = () => {
      console.log("Conexão SSE estabelecida");
    };
    eventSource.addEventListener("new_message", (e) => {
      try {
        const data = JSON.parse(e.data);
        console.log(data);
        setMessages((prevMessages) => [
          ...prevMessages,
          JSON.parse(data.message),
        ]);
      } catch (error) {
        console.error("Erro ao processar mensagem SSE:", error);
      }
    });

    // Lida com erros de conexão
    eventSource.onerror = (error) => {
      console.error("Erro na conexão SSE:", error);
      eventSource.close();
    };

    // Fecha a conexão quando o componente é desmontado
    return () => {
      eventSource.close();
    };
  }, []);

  return (
    <div className="dropdown dropdown-end">
      <div
        tabIndex={0}
        role="button"
        className="btn btn-ghost btn-circle btn-sm"
      >
        <div className="indicator">
          <MdNotifications className="text-xl" />
          <span className="badge badge-sm indicator-item badge-secondary">
            {messages?.length}
          </span>
        </div>
      </div>
      <div
        tabIndex={0}
        className="card card-compact dropdown-content overflow-auto max-h-72 w-96 bg-base-100 z-[1] mt-3 w-52 shadow"
      >
        <div className="card-body">
          <ul>
            {messages.reverse().map((msg, index) => (
              <li
                className="text-xs p-3 w-72 rounded-lg bg-base-200 mt-2"
                key={index}
              >
                <div className="bg-white p-4 rounded-lg shadow-md max-w-lg mx-auto">
                  <div className="flex justify-between items-center mb-4">
                    <p className="font-bold text-lg text-gray-800">
                      Pedido {msg.status}
                    </p>
                    <p className="text-xs text-gray-500">
                      {new Date(msg.created_at).toLocaleString()}
                    </p>
                  </div>

                  <div className="mb-4">
                    <p className="text-sm text-gray-600">
                      Cliente:{" "}
                      <span className="font-semibold">{msg.client_id}</span> -
                      Pedido:{" "}
                      <span className="font-semibold">{msg.request_id}</span>
                    </p>
                  </div>

                  <div className="flex justify-between items-center">
                    <p className="font-medium text-lg text-gray-700">Total:</p>
                    <p className="font-bold text-xl text-green-600">
                      {msg.total}
                    </p>
                  </div>
                </div>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
};

export default Messenger;
