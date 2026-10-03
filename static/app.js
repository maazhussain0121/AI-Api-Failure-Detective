async function loadIncidents() {

    const response = await fetch("/api/incidents");

    const incidents = await response.json();

    const container =
        document.getElementById("incidents");

    container.innerHTML = "";

    incidents.forEach(incident => {

        const div = document.createElement("div");

        div.className = "incident";

        div.innerHTML = `
            <div class="incident-header">

                <div>

                    <h3>
                        ${incident.id}
                    </h3>

                    <p>
                        ${incident.endpoint}
                    </p>

                    <p>
                        Service:
                        ${incident.service}
                    </p>

                </div>

                <div>

                    <strong
                        class="status status-${incident.status_code}"
                    >
                        HTTP ${incident.status_code}
                    </strong>

                    <br><br>

                    <button
                        onclick="investigate('${incident.id}')"
                    >
                        Investigate
                    </button>

                </div>

            </div>
        `;

        container.appendChild(div);

    });
}


async function investigate(id) {

    const section =
        document.getElementById("investigation");

    const result =
        document.getElementById("result");

    section.classList.remove("hidden");

    result.innerHTML = `
        <div class="loading">
            🤖 AI is investigating the incident...
        </div>
    `;

    const response = await fetch(
        `/api/incidents/${id}/investigate`,
        {
            method: "POST"
        }
    );

    const data = await response.json();

    renderResult(data);

    section.scrollIntoView({
        behavior: "smooth"
    });
}


function renderResult(data) {

    const incident = data.incident;
    const analysis = data.analysis;

    const result =
        document.getElementById("result");

    const evidence = (analysis.evidence || [])
        .map(item => `<li>✓ ${item}</li>`)
        .join("");

    const recommendations =
        (analysis.recommendations || [])
        .map(item => `<li>• ${item}</li>`)
        .join("");

    const failureChain =
        (analysis.failure_chain || [])
        .map(item => `<li>${item}</li>`)
        .join("");

    const logs =
        incident.logs
        .map(log => `<div>${log}</div>`)
        .join("");


    result.innerHTML = `

        <div class="card">

            <h3>Incident Information</h3>

            <p>
                <strong>Endpoint:</strong>
                ${incident.endpoint}
            </p>

            <p>
                <strong>Status:</strong>
                HTTP ${incident.status_code}
            </p>

            <p>
                <strong>Service:</strong>
                ${incident.service}
            </p>

        </div>


        <div class="card">

            <h3>AI Root Cause Analysis</h3>

            <div class="root-cause">

                <h3>
                    ${analysis.root_cause}
                </h3>

                <strong>
                    Confidence:
                    ${analysis.confidence}
                </strong>

            </div>

            <p>
                ${analysis.summary}
            </p>

        </div>


        <div class="card">

            <h3>Failure Chain</h3>

            <ol class="failure-chain">

                ${failureChain}

            </ol>

        </div>


        <div class="card">

            <h3>Evidence</h3>

            <ul class="evidence">

                ${evidence}

            </ul>

        </div>


        <div class="card">

            <h3>Recommendations</h3>

            <ul class="recommendations">

                ${recommendations}

            </ul>

        </div>


        <div class="card">

            <h3>Raw Logs</h3>

            <div class="logs">

                ${logs}

            </div>

        </div>

    `;
}


loadIncidents();