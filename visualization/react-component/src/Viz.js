import React, { useEffect } from 'react';
import { initialize } from './visualize.js';

const Viz = () => {

    useEffect(() => {
        initialize();
    }, []);

    return (
        // <div id="author-rank"></div>
        <div id="container-2" className="svg-container-2" />
    )
}

export default Viz;