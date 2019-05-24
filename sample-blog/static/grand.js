const App = angular.module('sampleApp', []);

App.config(['$interpolateProvider', function($interpolateProvider) {
    $interpolateProvider.startSymbol('((');
    $interpolateProvider.endSymbol('))');
}]);

App.service('$vault', function() {
    const self = this;

    self.check_session = function() {
        return fetch('/check_session')
            .then(resp => resp.json())
            .then(json => {
                self.online = json.online;
                self.you = json.user;
                return json;
            });
    }
});