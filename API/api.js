const API_url = 'http://127.0.0.1:5000/api/jobs'

const section_jobs = document.getElementById('all-jobs')
const company = document.getElementById('company')
const local = document.getElementById('local')

function getUrlJobs(){
    return fetch(API_url)
    .then((response) => response.json())
    .then((jsonres) => jsonres)
    .then((jsonresp) => {
        const jobs = jsonresp.map(describeJobs).join('')
        section_jobs.innerHTML += jobs
        company.innerHTML += jobs
    })
}

getUrlJobs()

function describeJobs(api){
    return `
    <section id="jobs">
        <h1 id="job-name">${api['job_title']}</h1>
        <div id="header-job">
            <h2 id="company">Empresa:${api['job_about']} </h2>
            <h2 id="local">Local: ${api['job_location']}</h2>
            <p id="job-date">Data da Publicação: ${api['job_post_date']}</p>
            <hr>
            <h2 id="contract-time">Tempo de contratação: ${api['job_contrat_time']}</h2>
            <h2 id="level">Level de Conhecimento</h2>
        </div>
        <div id="apply">
            <button>Apply</button>
        </div>
        <div id="about-job">
            <h2 id="requirements">Requerimentos:</h2>
                <ul id="">
                    <li>${api['job_requirements']}</li>
                </ul>
            <hr>
            <h2 id="description">Descrição do Trab:</h2>
                <ul id="">
                    <li>${api['job_other_skills']}</li>
                </ul>
            <hr>
            <h2 id="skills">Outras Skills:</h2>
                <ul id="">
                    <li>${api['job_other_skills']}</li>
                </ul>
        </div>
        <div id="about-company">
            <p>${api['job_about']}</p>
        </div>
        <hr>
    </section>
    `
}
    