App.controller('tagspageCtrl', ['$scope', '$vault', function($scope, $vault) {

    $scope.init = true;
    
    $scope.tags = [];
    $scope.is_loading = null;
    $scope.no_more_records = null;

    $scope.you = null;

    $scope.load_tags = function() {
        const tag_ids = $scope.tags.map(tag => tag.id);
        const min_tag_id = tag_ids.length ? Math.min(...tag_ids) : null;
        const path = min_tag_id ? `/get_latest_tags/${min_tag_id}` : '/get_latest_tags';

        $scope.is_loading = true;
        return fetch(path)
            .then(resp => resp.json())
            .then(json => {
                json.tags.forEach(tag => {
                    $scope.tags.push(tag);
                });
                if (json.tags.length < 5) {
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
                $scope.load_tags()
                .then(() => {
                    $scope.init = false;
                    $scope.$apply();
                });
            })
    });

}])