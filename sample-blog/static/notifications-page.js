App.controller('notespageCtrl', ['$scope', '$vault', function($scope, $vault) {

    $scope.init = true;
    
    $scope.notifications = [];
    $scope.min_notes_id = null;
    $scope.is_loading = null;
    $scope.no_more_records = null;

    $scope.you = null;

    $scope.load_notifications = function() {
        const notes_ids = $scope.notifications.map(notes => notes.id);
        $scope.min_notes_id = notes_ids.length ?
            Math.min(...notes_ids) :
            null;

        const path = $scope.min_notes_id ? 
        `/users/${$scope.you.id}/get_latest_notifications/${$scope.min_notes_id}` : 
        `/users/${$scope.you.id}/get_latest_notifications`;

        $scope.is_loading = true;
        return fetch(path)
            .then(resp => resp.json())
            .then(json => {
                json.notifications.forEach(notes => {
                    $scope.notifications.push(notes);
                });
                if (json.notifications.length < 5) {
                    $scope.no_more_records = true;
                }
                $scope.is_loading = false;
                $scope.$apply();
                console.log(json, $scope);
            });
    }

    $(document).ready(function() {
        $vault.check_session()
        .then(() => {
            $scope.you = $vault.you;
            $scope.load_notifications()
                .then(() => {
                    $scope.init = false;
                    $scope.$apply();
                });
        });
    });

}])