App.controller('userpageCtrl', ['$scope', '$vault', function($scope, $vault) {

    $scope.init = true;
    
    $scope.posts = [];
    $scope.min_post_id = null;
    $scope.is_loading = null;
    $scope.no_more_records = null;

    $scope.you = null;
    $scope.user = null;

    $scope.get_user = function() {
        const user_id = window.location.pathname.split('/').pop();
        return fetch(`/get_user_by_id/${user_id}`)
            .then(resp => resp.json())
            .then(json => {
                $scope.user = json.user;
                $scope.$apply();
                return json;
            })
            .catch(error => {
                console.log(error);
                $scope.user = false;
                $scope.$apply();
                throw error;
            });
    }

    $scope.load_user_posts = function() {
        const post_ids = $scope.posts.map(post => post.id);
        $scope.min_post_id = post_ids.length ?
            Math.min(...post_ids) :
            null;

        const path = $scope.min_post_id ? 
        `/users/${$scope.user.id}/get_latest_posts/${$scope.min_post_id}` : 
        `/users/${$scope.user.id}/get_latest_posts`;

        $scope.is_loading = true;
        return fetch(path)
            .then(resp => resp.json())
            .then(json => {
                json.posts.forEach(post => {
                    $scope.posts.push(post);
                });
                if (json.posts.length < 5) {
                    $scope.no_more_records = true;
                }
                $scope.is_loading = false;
                $scope.$apply();
                console.log(json, $scope);
            });
    }

    $(document).ready(function() {
        const check = $vault.check_session();
        const user = $scope.get_user();
        Promise.all([check, user]).then(values => {
            console.log(values);
            $scope.you = values[0].user;
            if($scope.user) {
                $scope.load_user_posts()
                .then(() => {
                    $scope.init = false;
                    $scope.$apply();
                });
            }
        })
    });

}])