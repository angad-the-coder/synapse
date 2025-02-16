import { H3Error, sendError } from "h3";

export default defineEventHandler(async (event) => {
  try {
    // @ts-ignore
    const { status, url } = await $fetch(`${process.env.TERRA_BASE_URL}/auth/generateWidgetSession`, {
      method: "POST",
      // @ts-ignore
      headers: {
        "x-api-key": process.env.TERRA_API_KEY,
        "dev-id": process.env.TERRA_DEV_ID,
        "Content-Type": "application/json"
      },
      body: {
        "providers": "GARMIN",
        "language": "en",
        "reference_id": "angad.bhargav@gmail.com",
        "auth_success_redirect_url": "http://localhost:3000/demo",
        "auth_failure_redirect_url": "http://localhost:3000/failure"
      },
    });
    return {
      status,
      url
    }
  } catch (error) {
    console.log(error);
    sendError(event, error as H3Error, false);
  }
});
