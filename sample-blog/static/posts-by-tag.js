App.controller('postsbytagCtrl', ['$scope', '$vault', function($scope, $vault) {

    let tag_id = null;

    $scope.tag_exists = null;
    $scope.init = true;
    $scope.posts_by_tag = [];
    $scope.is_loading = null;
    $scope.no_more_records = null;
    $scope.you = null;

    $scope.get_tag_by_id = function() {
        if (!tag_id || isNaN(tag_id)) {
            $scope.tag_exists = false;
            return;
        }

        const url = `/get_tag_by_id/${tag_id}`;
        
        return fetch(url)
            .then(resp => resp.json())
            .then(json => {
                $scope.tag_exists = json.tag;
                $scope.$apply();
                console.log(json, $scope);
            });
    }

    $scope.load_posts_by_tag = function() {
        const post_tags_ids = $scope.posts_by_tag.map(post_tag => post_tag.id);
        const min_post_tag_id = post_tags_ids.length ? Math.min(...post_tags_ids) : null;
        const path = $scope.min_post_id ? 
        `/tags/${tag_id}/get_latest_posts/${min_post_tag_id}` : 
        `/tags/${tag_id}/get_latest_posts`;

        $scope.is_loading = true;
        return fetch(path)
            .then(resp => resp.json())
            .then(json => {
                json.posts.forEach(post_by_tag => {
                    $scope.posts_by_tag.push(post_by_tag);
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
        tag_id = window.location.pathname.split('/').pop();
        $vault.check_session()
            .then(() => {
                $scope.get_tag_by_id().then(() => {
                    console.log($scope);
                    if (!!$scope.tag_exists) {
                        $scope.load_posts_by_tag()
                        .then(() => {
                            $scope.init = false;
                            $scope.$apply();
                        });
                    }
                });
            })
    });

}])