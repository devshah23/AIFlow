import { Route, Routes } from "react-router-dom";
import Chat from "./views/Chat";
import Home from "./views/Home";
import CreateFlow from "./views/CreateFlow";
import Layout from "./components/layouts/MainLayout";
import { Slide, ToastContainer } from "react-toastify";

export default function App() {
  return (
    <div className="min-h-screen min-w-full bg-[var(--background)] flex flex-col">
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Home />} />
          <Route path="/create/:id" element={<CreateFlow />} />
          <Route path="/create/" element={<CreateFlow />} />
          <Route path="/chat" element={<Chat />} />
        </Route>
      </Routes>
      <ToastContainer
        toastClassName={"!text-sm"}
        autoClose={1500}
        hideProgressBar={true}
        position="top-center"
        transition={Slide}
      />
    </div>
  );
}
