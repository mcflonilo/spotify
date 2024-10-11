import {redirectToAuthCodeFlow} from "./redirectToAuthCodeFlow.ts";
import {getAccessToken} from "./getAccessToken.ts";
import {fetchProfile} from "./fetchProfile.ts";
import {populateUI} from "./populateUI.ts";

const clientId = "f38377398eb14acdaf4366d72642faf9";
const params = new URLSearchParams(window.location.search);
const code = params.get("code");

if (!code) {
    redirectToAuthCodeFlow(clientId);
} else {
    const accessToken = await getAccessToken(clientId, code);
    const profile = await fetchProfile(accessToken);
    console.log(profile);
    populateUI(profile);
}