import React, { Component } from 'react';
import './InputArea.css'; 
import { isMobile } from 'react-device-detect';
import { MContext } from './MyProvider';


export class InputArea extends Component {

    static contextType = MContext;

    constructor(props) {
        super(props);
        this.textAreaRef = React.createRef();
        this.submitTextToBackend = this.submitTextToBackend.bind(this);
    }

    getFormID() {
        return isMobile? "inputAreaContainerMobile" : "inputAreaContainer";
    }

    async postData(url = '', data = {}) {
        const response = await fetch(url, {
            method: 'POST',
            body: data, 
        });
        return await response.text(); 
    }

    async submitTextToBackend() {
        
        if (this.textAreaRef.current.value.length === 0) {
            this.context.setMessage("Input text cannot be empty. Please enter text and try again.");
            console.log("Input text cannot be empty. Please enter text and try again.");
            return null;
        }

        let data = new FormData();
        data.append('inputText', this.textAreaRef.current.value);

        console.log(`Sending ${this.textAreaRef.current.value} to backend`)

        try {
            this.context.setAnimationRunning(true);
            // const processedResponse = await this.postData('https://quantumstatic.pythonanywhere.com/sendText', data);
            const processedResponse = await this.postData('http://127.0.0.1:5000/sendText', data);
            console.log(`Server responded with ${processedResponse}`);
            this.context.setMessage(processedResponse.length > 0 ? processedResponse : "Something went wrong. Please try again later.");
        } catch {
            this.context.setMessage("Something went wrong, data could not be sent to the server. Please try again later.");
        }
        this.context.setAnimationRunning(false);
    }

    render() {

        return (
            <React.Fragment>
                <fieldset id = {this.getFormID()} className="MyFieldset">
                    <legend align="left">Input Area</legend>
                        <form>
                            {/* Text Box Code */}
                            <label htmlFor = "inputText" /> 
                            <textarea name= "inputText" id="inputText" placeholder="Paste your text here..." ref={this.textAreaRef} autoComplete="on" required autoFocus/>

                            <br />

                            {/* Submit/Reset Button Code */}
                            <button type="button" formNoValidate onClick = {this.submitTextToBackend}>Submit</button>
                            <button type='reset'>Reset</button>
                        </form>
                    
                        {/* Upload File Code */}

                </fieldset>
            </React.Fragment>
        );
    }
}

export default InputArea;