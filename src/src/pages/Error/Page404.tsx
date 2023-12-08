import { IconButton } from "@mui/material";
import { useNavigate } from "react-router-dom";
import HomeIcon from "@mui/icons-material/Home";

function Page404() {
  const navigator = useNavigate();

  return (
    <>
      <div>
        <h1>ERROR 404 PÁGINA NO ENCONTRADA</h1>
        <IconButton onClick={() => navigator("/")}>
          <HomeIcon />
        </IconButton>
      </div>
    </>
  );
}

export default Page404;
