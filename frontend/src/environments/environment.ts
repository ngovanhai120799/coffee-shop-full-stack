/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'dev-q2lpx6g5puuouis8', // the auth0 domain prefix
    audience: 'coffee-jwt', // the audience set for the auth0 app
    clientId: 'JLrpRYuCSrXPHBKA4gy5Z1UeubAJ45Bf', // the client id generated for the auth0 app
    callbackURL: 'http://127.0.0.1:8100', // the base url of the running ionic application.
  }
};
