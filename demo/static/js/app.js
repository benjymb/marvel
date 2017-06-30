/**
 * Created by benjy on 6/29/17.
 */
angular.element(document).ready(function () {
    componentHandler.upgradeAllRegistered();
});

angular.module('demoApp', [])
    .config(['$interpolateProvider',
        function ($interpolateProvider) {
            $interpolateProvider.startSymbol('[[').endSymbol(']]');
        }
    ])
    .controller('MainAppController', function ($scope) {
        $scope.currentAction = '';
        $scope.searchMode = false;
        $scope.selectedIndex = 0;
        $scope.buttonMode = 'search';
        $scope.changeIndex = function (newValue) {
            $scope.selectedIndex = newValue;
        };
        $scope.changeMode = function(){
            if (!$scope.searchMode) {
                $scope.searchMode = true;
                $scope.selectedIndex = 2;
                $scope.buttonMode = 'close';
            } else {
                $scope.searchMode = false;
                $scope.selectedIndex = 0;
                $scope.buttonMode = 'search';
            }
        };
    })
    .controller('MostPopularAppController', function ($scope) {
        $scope.recentSearches = [];
        $scope.characters = [];
        $scope.popularCharacters = [];
    });

