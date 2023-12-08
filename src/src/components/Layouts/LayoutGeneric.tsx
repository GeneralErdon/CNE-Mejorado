import { Outlet } from "react-router-dom";

function LayoutGeneric() {

  return (<>
  <div>
    <Outlet />
  </div>
  </>)
}

export default LayoutGeneric;