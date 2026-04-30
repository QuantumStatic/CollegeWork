import React, { Component } from 'react';
import { MContext } from './MyProvider';
import "./ArrowPointer.css";

export class ArrowPointer extends Component {

    static contextType = MContext;

    constructor(props) {
        super(props);
        this.startAnimation = this.startAnimation.bind(this);
    }

    startAnimation() {
        if (this.context.state.animationRunning) {
            return "filled"
        }
        return "";
    }
    

    render() {
        return (
            <React.Fragment>
                <div className="arrow-container">
                    <div className={`arrow ${this.startAnimation()}`}>
                        <div className="arrow-top" />
                        <div className="arrow-middle" />
                        <div className="arrow-bottom" />
                    </div>
                </div>
            </React.Fragment>
        );
    }
}

export default ArrowPointer;