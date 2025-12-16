


const USERNAME="octocat";
const PER_PAGE= 5;
const APINAME="github.com";

async function fetchAllPublicRepos()
{
    try{
        let url = `https://api.github.com/users/${USERNAME}/repos?page=1&per_page=${PER_PAGE}`;

        let page = 1;


        while (url) {
        console.log(`\nFetching Page ${page}: ${url}`);


        const res = await fetch(url);
        const data = await res.json();


        // Print repo names for clarity
        data.forEach(repo => {
        console.log(`- ${repo.name}`);
        });


        // Read the Link header
        const linkHeader = res.headers.get("link");
        url = extractNext(linkHeader);


        page++;
        }


        console.log("\nNo more pages.");
    }
    catch(error)
    {
        console.log(error.message);
    }
}


    // Extracts only the `next` relation from the Link header
function extractNext(linkHeader) {
    if (!linkHeader) return null;


    const match = linkHeader.match(/<([^>]+)>; rel="next"/);
    return match ? match[1] : null;
}


fetchAllPublicRepos().catch(err => console.error(err));
