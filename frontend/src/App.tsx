import { createBrowserRouter, RouterProvider } from "react-router-dom";
import Chat from "./views/Chat";
import Home from "./views/Home";
import CreateFlow from "./views/CreateFlow";
import Layout from "./components/layouts/MainLayout";
import { Slide, ToastContainer } from "react-toastify";

const router = createBrowserRouter([
  {
    path: "/",
    element: <Layout />,
    children: [
      {
        index: true,
        element: <Home />,
      },
      {
        path: "create",
        element: <CreateFlow />,
      },
      {
        path: "create/:id",
        element: <CreateFlow />,
      },
      {
        path: "chat",
        element: <Chat />,
      },
      {
        path: "chat/:id",
        element: <Chat />,
      },
    ],
  },
]);

export default function App() {
  return (
    <div className="min-h-screen min-w-full bg-[var(--background)] flex flex-col">
      {/* <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Home />} />
          <Route path="/create/:id" element={<CreateFlow />} />
          <Route path="/create/" element={<CreateFlow />} />
          <Route path="/chat/" element={<Chat />} />
          <Route path="/chat/:id" element={<Chat />} />
        </Route>
      </Routes> */}
      <RouterProvider router={router} />
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
