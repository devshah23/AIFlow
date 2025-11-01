import { Outlet } from "react-router-dom";
import { Navbar01 as Navbar } from "../ui/shadcn-io/navbar-01";
import { navigationLinks } from "@/configs/NavLinkConfig";
import AIFlowLogo from "@/assets/AIFlowLogo.png";
const Layout = () => {
  const CompanyLogo = (
    <img src={AIFlowLogo} alt="AIFlow Main Logo" className="h-12 w-auto" />
  );
  return (
    <>
      <Navbar navigationLinks={navigationLinks} logo={CompanyLogo} />
      <main className="max-h-[calc(100vh-64px)] h-full w-full flex-grow pt-2 mx-auto px-2">
        <Outlet />
      </main>
    </>
  );
};

export default Layout;
