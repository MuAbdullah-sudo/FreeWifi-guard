//
// UPDATE DASHBOARD STATS
//

function updateDashboardStats(data) {

    animateCounter(
        "total-networks",
        data.length
    );

    const safeCount =
        data.filter(
            n => n.risk === "SAFE"
        ).length;

    animateCounter(
        "safe-networks",
        safeCount
    );

    const suspiciousCount =
        data.filter(
            n => n.risk === "SUSPICIOUS"
        ).length;

    animateCounter(
        "suspicious-networks",
        suspiciousCount
    );

    const dangerousCount =
        data.filter(
            n => n.risk === "DANGEROUS"
        ).length;

    animateCounter(
        "dangerous-networks",
        dangerousCount
    );
}


/* ===================================== */
/* COUNTER ANIMATION */
/* ===================================== */

function animateCounter(id, target) {

    const element =
        document.getElementById(id);

    let current = 0;

    const increment =
        target / 30;

    const timer = setInterval(() => {

        current += increment;

        if (current >= target) {

            current = target;

            clearInterval(timer);
        }

        element.innerText =
            Math.floor(current);

    }, 25);
}


/* ===================================== */
/* CREATE NETWORK CARD */
/* ===================================== */

function createNetworkCard(network) {

    let riskClass = "safe";

    if (network.risk === "SUSPICIOUS") {

        riskClass = "suspicious";
    }

    if (network.risk === "DANGEROUS") {

        riskClass = "dangerous";
    }

    return `

        <div class="network-card ${riskClass}">

            <p>
                <strong>SSID:</strong>
                ${network.ssid || "Unknown"}
            </p>

            <p>
                <strong>BSSID:</strong>
                ${network.bssid || "Unknown"}
            </p>

            <p>
                <strong>Signal:</strong>
                ${network.signal || "Unknown"}
            </p>

            <p>
                <strong>Security:</strong>
                ${network.security || "Unknown"}
            </p>

            <p>
                <strong>Risk:</strong>
                ${network.risk || "SAFE"}
            </p>

        </div>
    `;
}


/* ===================================== */
/* RENDER RESULTS */
/* ===================================== */

function renderResults(title, data) {

    const resultsDiv =
        document.getElementById("results");

    updateDashboardStats(data);

    let html = `

        <div class="results-header">

            <h2>
                ${title}
            </h2>

        </div>
    `;

    data.forEach(network => {

        html += createNetworkCard(network);

    });

    resultsDiv.innerHTML = html;
}


/* ===================================== */
/* SCAN NETWORKS */
/* ===================================== */

async function scanNetworks() {

    const resultsDiv =
        document.getElementById("results");

    resultsDiv.innerHTML = `

        <div class="loading">
            Scanning Networks...
        </div>
    `;

    try {

        const response =
            await fetch("/scan");

        const data =
            await response.json();

        renderResults(
            "Nearby Networks",
            data
        );

    } catch (error) {

        console.error(error);

        resultsDiv.innerHTML = `

            <div class="network-card dangerous">

                <h3 style="color:red;">
                    Scan Failed
                </h3>

                <p>
                    Unable to scan Wi-Fi networks.
                </p>

            </div>
        `;
    }
}


/* ===================================== */
/* VIEW HISTORY */
/* ===================================== */

async function loadHistory() {

    const resultsDiv =
        document.getElementById("results");

    resultsDiv.innerHTML = `

        <div class="loading">
            Loading History...
        </div>
    `;

    try {

        const response =
            await fetch("/history");

        const data =
            await response.json();

        renderResults(
            "Scan History",
            data
        );

    } catch (error) {

        console.error(error);

        resultsDiv.innerHTML = `

            <div class="network-card dangerous">

                <h3 style="color:red;">
                    Failed to Load History
                </h3>

            </div>
        `;
    }
}


/* ===================================== */
/* BUTTON EVENTS */
/* ===================================== */

document.getElementById("scan-btn")
.addEventListener(
    "click",
    scanNetworks
);

document.getElementById("history-btn")
.addEventListener(
    "click",
    loadHistory
);


/* ===================================== */
/* AUTO LIVE SCAN */
/* ===================================== */

setInterval(() => {

    scanNetworks();

}, 30000);


/* ===================================== */
/* LIVE ALERT MONITOR */
/* ===================================== */

async function loadAlerts() {

    try {

        const response =
            await fetch("/alerts");

        const alerts =
            await response.json();

        const container =
            document.getElementById(
                "alerts-container"
            );

        if (!alerts.length) {

            container.innerHTML = `

                <div class="alert-card info-alert">

                    No suspicious activity detected.

                </div>
            `;

            return;
        }

        let html = "";

        alerts.forEach(alert => {

            let alertClass =
                "info-alert";

            if (alert.level === "warning") {

                alertClass =
                    "warning-alert";
            }

            if (alert.level === "danger") {

                alertClass =
                    "danger-alert";
            }

            html += `

                <div class="alert-card ${alertClass}">

                    <strong>
                        [${alert.time}]
                    </strong>

                    ${alert.type}

                    -

                    ${alert.message}

                </div>
            `;
        });

        container.innerHTML = html;

    } catch (error) {

        console.error(
            "ALERT ERROR:",
            error
        );
    }
}


/* ===================================== */
/* LOAD ALERTS EVERY 3 SECONDS */
/* ===================================== */

setInterval(loadAlerts, 3000);

loadAlerts();


/* ===================================== */
/* CYBER PARTICLE ENGINE */
/* ===================================== */

const particlesContainer =
    document.getElementById("particles");

function createParticle() {

    const particle =
        document.createElement("div");

    particle.classList.add("particle");

    const size =
        Math.random() * 6 + 2;

    particle.style.width =
        `${size}px`;

    particle.style.height =
        `${size}px`;

    particle.style.left =
        `${Math.random() * 100}%`;

    particle.style.animationDuration =
        `${Math.random() * 8 + 6}s`;

    particle.style.opacity =
        Math.random();

    particlesContainer.appendChild(
        particle
    );

    setTimeout(() => {

        particle.remove();

    }, 14000);
}


// Generate particles
setInterval(createParticle, 120);


/* ===================================== */
/* MOUSE GLOW */
/* ===================================== */

const glow =
    document.createElement("div");

glow.classList.add("mouse-glow");

document.body.appendChild(glow);


document.addEventListener(
    "mousemove",
    e => {

        glow.style.left =
            `${e.clientX}px`;

        glow.style.top =
            `${e.clientY}px`;
    }
);


/* ===================================== */
/* SUBTITLE TYPING EFFECT */
/* ===================================== */

const subtitle =
    document.querySelector(".subtitle");

const originalText =
    subtitle.innerText;

subtitle.innerText = "";

let index = 0;

function typeSubtitle() {

    if (index < originalText.length) {

        subtitle.innerText +=
            originalText.charAt(index);

        index++;

        setTimeout(
            typeSubtitle,
            40
        );
    }
}

typeSubtitle();

