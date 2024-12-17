import React, { useEffect, useState } from 'react';
import { MdNotifications } from 'react-icons/md';

const Messenger: React.FC = () => {
  const [messages, setMessages] = useState<string[]>([]);

  useEffect(() => {
    // Conecta ao servidor Flask-SSE
    const eventSource = new EventSource("http://localhost:5000/stream");
    eventSource.onopen = () => {
      console.log("Conexão SSE estabelecida");
    };
    eventSource.addEventListener("new_message", (e) => {   
    try {
      const data = JSON.parse(e.data);
      setMessages((prevMessages) => [...prevMessages, data.message]);
    } catch (error) {
      console.error("Erro ao processar mensagem SSE:", error);
    }})
  

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
          <div tabIndex={0} role="button" className="btn btn-ghost btn-circle btn-sm">
            <div className="indicator">
              <MdNotifications className='text-xl' />
              <span className="badge badge-sm indicator-item badge-secondary">{messages?.length}</span>
            </div>
          </div>
          <div
            tabIndex={0}
            className="card card-compact dropdown-content bg-base-100 z-[1] mt-3 w-52 shadow"
          >
            <div className="card-body">
              <ul>
                {messages.map((msg, index) => (
                  <li key={index}>{msg}</li>
                ))}
              </ul>
            </div>
          </div>
        </div>
  );
};

export default Messenger;
