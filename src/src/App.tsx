import { BrowserRouter, Route, Routes } from 'react-router-dom'
import Home from 'src/pages/Home';
import Page404 from 'src/pages/Error/Page404';
function App() {
  

  return (
    <BrowserRouter>
      <Routes>
        <Route path='/' >
          <Route index element={<Home />} />
          <Route path='*' element={<Page404/>} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App
