"use client";

import ChatBot from "react-chatbotify";

export default function Home() {
  const flow = {
    start: {
      message: "Salut! Cum te cheama?",
      path: "end",
    },
    end: {
      message: (params: any) => `Ma bucur de cunostinta, ${params.userInput}!`,
      chatDisabled: true,
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
