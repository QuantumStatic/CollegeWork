import React, { Component } from 'react'
import { isMobile } from 'react-device-detect';
import { MContext } from './MyProvider';
import './OutputBox.css';

class OutputBox extends Component {

    static contextType = MContext;

    getOutputAreaContainerID() {
        if (isMobile) {
            return "ouputAreaContainerMobile";
        } else {
            return "ouputAreaContainer";
        }
    }

    render() {
        return (
            <React.Fragment>
                
                <fieldset id={this.getOutputAreaContainerID()} className="MyFieldset">
                    <legend align="left">Output Area</legend>
                    <div id="outputTextBox">
                        {this.context.state.animationRunning ? "Processing your input..." :this.context.state.message}
                    </div>
                </fieldset>

            </React.Fragment>
        );
    }
}

export default OutputBox;