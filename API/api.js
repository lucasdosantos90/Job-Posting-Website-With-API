const API_url = 'https://lucasds90.pythonanywhere.com/api/jobs'

const section_jobs = document.getElementById('all-jobs')
const company = document.getElementById('company')
const local = document.getElementById('local')

function getUrlJobs(){
    return fetch(API_url,{ method: 'get', mode: 'cors' })
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
            <h2 id="company">Company: ${api['job_about']} </h2>
            <h2 id="local">Local: ${api['job_location']}</h2>
            <hr>
            <h2 id="requirements">Requirements: </h2>
                <ul id="">
                    <li>${api['job_requirements']}</li>
                </ul>
        </div>
        <hr>
        <div id="about-job">
            <h2 id="description">Job Description: </h2>
                <ul id="">
                    <li>${api['job_other_skills']}</li>
                </ul>
            <hr>
            <h2 id="skills">Other Skills: </h2>
                <ul id="">
                    <li>${api['job_other_skills']}</li>
                </ul>
        </div>
        <div id="about-company">
            <p>${api['job_about']}</p>
        </div>
        <div id="apply">
            <button onclick="location.href='mailto:${api['job_apply']}';">Apply</button>
        </div>
        <hr>
    </section>
    `
}
