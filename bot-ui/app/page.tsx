"use client";

import ChatBot from "react-chatbotify";

export default function Home() {
  async function fetchData(human_message: string) {
    try {
      const body = { human_message: human_message };

      const response = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(body),
      });

      const data = await response.json();

      return data.ai_message;
    } catch (error) {
      return (
        "Eroare de server. A fost inregistrata si va fi remediata in curand. " +
        "Va rugam sa incercati din nou mai tarziu."
      );
    }
  }

  const flow = {
    start: {
      message: "Buna ziua! Cu ce va pot ajuta?",
      path: "loop",
    },
    loop: {
      message: async (params: any) => await fetchData(params.userInput),
      path: "loop",
    },
  };

  return (
    <ChatBot
      settings={{
        general: { embedded: true },
        footer: { text: "" },
        header: { title: "Claudiu", showAvatar: false },
      }}
      flow={flow}
    />
  );
}
