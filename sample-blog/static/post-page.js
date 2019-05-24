App.controller('postpageCtrl', ['$scope', '$vault', function($scope, $vault) {

    $scope.init = true;
    
    $scope.post = null;
    $scope.comments = [];
    $scope.min_comment_id = null;
    $scope.is_loading = null;
    $scope.no_more_records = null;

    $scope.you = null;
    $scope.user = null;

    $scope.get_post = function() {
        const post_id = window.location.pathname.split('/').pop();
        return fetch(`/get_post_by_id/${post_id}`)
            .then(resp => resp.json())
            .then(json => {
                $scope.post = json.post;
                $scope.$apply();
                return json;
            })
            .catch(error => {
                console.log(error);
                $scope.post = false;
                $scope.$apply();
                throw error;
            });
    }

    $scope.load_post_comments = function() {
        const comment_ids = $scope.comments.map(comment => comment.id);
        $scope.min_comment_id = comment_ids.length ?
            Math.min(...comment_ids) :
            null;

        const path = $scope.min_comment_id ? 
        `/posts/${$scope.post.id}/get_latest_comments/${$scope.min_comment_id}` : 
        `/posts/${$scope.post.id}/get_latest_comments`;

        $scope.is_loading = true;
        return fetch(path)
            .then(resp => resp.json())
            .then(json => {
                json.comments.forEach(comment => {
                    $scope.comments.push(comment);
                });
                if (json.comments.length < 5) {
                    $scope.no_more_records = true;
                }
                $scope.is_loading = false;
                $scope.$apply();
                console.log(json, $scope);
            });
    }

    $(document).ready(function() {
        const check = $vault.check_session();
        const post = $scope.get_post();
        Promise.all([check, post]).then(values => {
            console.log(values);
            $scope.you = values[0].user;
            if($scope.post) {
                $scope.load_post_comments()
                .then(() => {
                    $scope.init = false;
                    $scope.$apply();
                });
            }
        })
    });

}])