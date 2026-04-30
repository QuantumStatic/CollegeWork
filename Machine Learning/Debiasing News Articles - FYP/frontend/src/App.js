import './App.css';
import "./Main.css";
import { isMobile } from 'react-device-detect';

import WebsiteHeader from './components/WebsiteHeader';
import InputArea from './components/InputArea';
import ArrowPointer from './components/ArrowPointer';
import OutputBox from './components/OutputBox';
import WebsiteFooter from './components/WebsiteFooter';
import MyProvider from './components/MyProvider';

function getArrowPointerID() {
  return isMobile? "ArrowPointerMobile" : "ArrowPointer";
}

function App() {
  return (
    <div className="App">

      <section id = "WebsiteHeader">
        <WebsiteHeader />
      </section>

      <hr />

      <div id = "myAppBody">
        <MyProvider>
          <section id = "InputArea">
            <InputArea />
          </section>

          <section id = {getArrowPointerID()}>
            <ArrowPointer />
          </section>

          <section id = "OutputArea">
            <OutputBox />
          </section>
        </MyProvider>   

      </div>

      <section id = "WebsiteFooter">
          <WebsiteFooter />
      </section>
    </div>
  );
}

export default App;
