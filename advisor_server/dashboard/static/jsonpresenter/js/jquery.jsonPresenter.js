/**
 * jQuery Json Presenter Plugin v1.0.0
 *
 * Copyright 2014 Steven Pease
 * Released under the MIT license:
 *   http://www.opensource.org/licenses/mit-license.php
 */
( function( $ ) {
	/**
	 * @param numberOfIndents
	 */
	function getIndentString( numberOfIndents ) {
		if ( typeof numberOfIndents === "undefined" ) {
			numberOfIndents = 1;
		}

		var result = '';
		for ( var i = 0; i < numberOfIndents; i++ ) {

			// Use two spaces to represent an indentation
			result += '  ';
		}
		return result;
	}

	function isJsonArray( jsonValue ) {
		return jsonValue && typeof jsonValue === 'object' && typeof jsonValue.length === 'number' && !jsonValue.propertyIsEnumerable( 'length' );
	}

	/**
	 * @param {unknown_type} jsonValue The JSON value to test
	 * @return {Boolean} Whether the provided JSON value is a Date object
	 */
	var isJsonDate = ( function() {
		var dateObject = new Date();

		return function( jsonValue ) {
			return jsonValue && jsonValue.constructor === dateObject.constructor;
		};
	} )();

	/**
	 * @param {unknown_type} jsonValue The JSON value to test
	 * @return {Boolean} Whether the provided JSON value is a NULL value
	 */
	var isJsonNull = function( jsonValue ) {
		return jsonValue === null;
	};

	/**
	 * @param {unknown_type} jsonValue The JSON value to test
	 * @return {Boolean} Whether the provided JSON value is a RegExp object
	 */
	var isJsonRegExp = ( function() {
		var regExpObject = new RegExp();

		return function( jsonValue ) {
			return jsonValue && jsonValue.constructor === regExpObject.constructor;
		};
	} )();

	function processJsonPrimitive( className, value, alternateDisplayValue ) {
		var cleanValue = function( value ) {
			var result = value;

			// Remove any "<" or ">" characters that could be interpretted as HTML
			if ( typeof result === 'string' ) {
				result = result.replace( /</g, '&lt;' ).replace( />/g, '&gt;' );
			}

			return result;
		};

		if ( alternateDisplayValue ) {
			value = '<span>' + cleanValue( value ) + '</span><span class="hidden">' + cleanValue( alternateDisplayValue ) + '</span>';
		} else {
			value = cleanValue( value );
		}

		return '<span class="parsed-json-value-' + className + ( alternateDisplayValue ? ' parsed-json-has-alternate-value' : '' ) + '">' + value + '</span>';
	}

	function processJsonValue( settings, jsonValue, indentLevel, propertyName ) {
		if ( typeof indentLevel === 'undefined' ) {
			indentLevel = 0;
		}

		var isExpandable = false,
			isToggleable = false,
			result = '';

		if ( isJsonArray( jsonValue ) ) {
			if ( jsonValue.length ) {
				result += '<span class="parsed-json-array-bracket">[</span><span class="parsed-json-expandable-ellipsis hidden">...</span><span class="parsed-json-expandable">';

				for ( var i = 0; i < jsonValue.length; i++ ) {
					result += processJsonValue( settings, jsonValue[ i ], indentLevel + 1 );

					if ( i < jsonValue.length - 1 ) {
						result += '<span class="parsed-json-object-comma">,</span>';
					}
				}

				result += "\n" + getIndentString( indentLevel ) + '</span><span class="parsed-json-array-bracket">]</span>';
				isExpandable = true;
			} else {
				result += '<span class="parsed-json-array-bracket">[]</span>';
			}
		} else {
			var valueType = typeof jsonValue;

			switch ( valueType ) {
				case 'object':
					if ( isJsonNull( jsonValue ) ) {
						result += processJsonPrimitive( 'null', null );
					} else if ( isJsonDate( jsonValue ) ) {
						result += processJsonPrimitive( 'date', 'new Date(' + jsonValue.getTime() + ')', jsonValue.toString() );
						isToggleable = true;
					} else if ( isJsonRegExp( jsonValue ) ) {
						result += processJsonPrimitive( 'regexp', jsonValue );
					} else {

						// Determine the number of properties this object has
						var propertyCount = ( function() {
							var result = 0;
							for ( var i in jsonValue ) { // jshint ignore:line
								result++;
							}
							return result;
						} )();

						if ( propertyCount > 0 ) {
							result += '<span class="parsed-json-object-bracket">{</span><span class="parsed-json-expandable-ellipsis hidden">...</span><span class="parsed-json-expandable">';
							( function() {
								var propertyCounter = 0;
								for ( var propertyName in jsonValue ) {
									result += processJsonValue( settings, jsonValue[ propertyName ], indentLevel + 1, propertyName );

									if ( ++propertyCounter < propertyCount ) {
										result += '<span class="parsed-json-object-comma">,</span>';
									}
								}
							} )();
							result += "\n" + getIndentString( indentLevel ) + '</span><span class="parsed-json-object-bracket">}</span>';
							isExpandable = true;
						} else {
							result += '<span class="parsed-json-object-bracket">{}</span>';
						}
					}
				break;
				case 'number':
					result += processJsonPrimitive( 'number', jsonValue );
				break;
				case 'boolean':
					result += processJsonPrimitive( 'boolean', jsonValue );
				break;
				case 'function':
					var expandedFunction = ( jsonValue.toString() ).replace( /\n/g, "\n" + getIndentString( indentLevel ) ),
						nonExpandedFunction = ( jsonValue.toString() ).replace( /\s+/g, ' ' );

					if ( expandedFunction !== nonExpandedFunction ) {
						result += processJsonPrimitive( 'function', nonExpandedFunction, expandedFunction );
						isToggleable = true;
					} else {
						result += processJsonPrimitive( 'function', nonExpandedFunction );
					}
				break;
				case 'undefined':
					result += processJsonPrimitive( 'undefined', jsonValue );
				break;
				default:
					var displayValue = '"' + jsonValue.replace( /\n/g, "\\n" ) + '"',
						alternateDisplayValue = '"' + jsonValue + '"';

					if ( displayValue !== alternateDisplayValue ) {
						result += processJsonPrimitive( 'string', displayValue, alternateDisplayValue );
						isToggleable = true;
					} else {
						result += processJsonPrimitive( 'string', displayValue );
					}

				break;
			}
		}

		var resultPrefix = ( indentLevel !== 0 ? "\n" : '' ) + getIndentString( indentLevel );
		if ( typeof propertyName !== 'undefined' ) {
			var propertyNameLabel = settings.wrapPropertiesInQuotes ? '"' + propertyName + '"' : propertyName;
			resultPrefix += '<span class="parsed-json-property-name' + ( isExpandable ? ' parsed-json-property-expandable' : '' ) + ( isToggleable ? ' parsed-json-property-toggleable' : '' ) + '">' + propertyNameLabel + '</span>: ';
		}

		result = resultPrefix + result;

		if ( isExpandable || isToggleable ) {
			return '<span class="' + ( isToggleable ? 'parsed-json-node-toggleable ' : '' ) + ( isExpandable ? 'parsed-json-node-expandable ' : '' ) + '">' + result + '</span>';
		} else {
			return result;
		}
	}

	function expandNode( expandableNodeElement ) {
		if ( expandableNodeElement.children( '.parsed-json-expandable' ).is( ':not(:visible)' ) ) {
			toggleExpandNode( expandableNodeElement );
		}
	}

	function collapseNode( expandableNodeElement ) {
		if ( expandableNodeElement.children( '.parsed-json-expandable' ).is( ':visible' ) ) {
			toggleExpandNode( expandableNodeElement );
		}
	}

	function toggleExpandNode( expandableNodeElement ) {
		expandableNodeElement.children( '.parsed-json-expandable,.parsed-json-expandable-ellipsis' ).toggleClass( 'hidden' );
	}

	function togglePresentationNode( toggleableNodeElement ) {
		toggleableNodeElement.children( '.parsed-json-has-alternate-value' ).find( 'span' ).toggleClass( 'hidden' );
	}

	function getExpandableChildNodes( expandableNodeElement ) {
		return expandableNodeElement.find( '> .parsed-json-expandable > .parsed-json-node-expandable' );
	}

	function expandAll( expandableElement ) {
		expand( expandableElement );
	}

	function collapseAll( expandableElement ) {
		collapse( expandableElement );
	}

	function expand( expandableNodeElement, depth ) {
		expandNode( expandableNodeElement );
		if ( !( typeof depth === 'number' && depth <= 0 ) ) {
			getExpandableChildNodes( expandableNodeElement ).each( function() {
				expandNode( $( this ) );
				expand( $( this ), typeof depth !== 'undefined' ? depth - 1 : depth );
			} );
		}
	}

	function collapse( expandableNodeElement, depth ) {
		if ( !( typeof depth === 'number' && depth <= 0 ) ) {
			getExpandableChildNodes( expandableNodeElement ).each( function() {
				collapse( $( this ), typeof depth !== 'undefined' ? depth - 1 : depth );
				collapseNode( $( this ) );
			} );
		}
		collapseNode( expandableNodeElement );
	}

	function getRootNode( containerElement ) {
		return containerElement.find( '> .parsed-json > .parsed-json-node-expandable' );
	}

	function onToggleableValueClick( event ) {
		togglePresentationNode( $( $( event.currentTarget ).parents( '.parsed-json-node-toggleable' ).get( 0 ) ) );
		event.stopPropagation();
	}

	function onExpandableValueClick( event ) {
		toggleExpandNode( $( $( event.currentTarget ).parents( '.parsed-json-node-expandable' ).get( 0 ) ) );
		event.stopPropagation();
	}

	function onExpandablePropertyClick( event ) {
		toggleExpandNode( $( event.currentTarget ).parent() );
		event.stopPropagation();
	}

	function onToggleablePropertyClick( event ) {
		togglePresentationNode( $( event.currentTarget ).parent() );
		event.stopPropagation();
	}

	function destroy( containerElement ) {
		containerElement
		.off( 'click', '.parsed-json-has-alternate-value span', onToggleableValueClick )
		.off( 'click', '.parsed-json-property-expandable', onExpandablePropertyClick )
		.off( 'click', '.parsed-json-expandable-ellipsis', onExpandableValueClick )
		.off( 'click', '.parsed-json-property-toggleable', onToggleablePropertyClick );

		containerElement.html( '' );
	}

	function create( containerElement, settings ) {

		// Make sure that the JSON Presenter is not stacking event listeners on top of existing ones
		if ( isAlreadyPresentingJson( containerElement ) ) {
			destroy( containerElement );
		}

		containerElement
		.on( 'click', '.parsed-json-has-alternate-value span', onToggleableValueClick )
		.on( 'click', '.parsed-json-property-expandable', onExpandablePropertyClick )
		.on( 'click', '.parsed-json-expandable-ellipsis', onExpandableValueClick )
		.on( 'click', '.parsed-json-property-toggleable', onToggleablePropertyClick );

		containerElement.html( '<pre class="parsed-json">' + processJsonValue( settings, settings.json ) + '</pre>' );
	}

	/**
	 * @param {DOMNode} containerElement The container element to check whether it already has JSON being presented within it
	 * @return {Boolean} Whether the provided container element already has JSON being presented within it
	 */
	function isAlreadyPresentingJson( containerElement ) {
		return !!containerElement.find( '> pre.parsed-json' ).length;
	}

	$.fn.jsonPresenter = function( options ) {
		if ( options && typeof options === 'object' ) {
			var defaults = {
				json: {},
				wrapPropertiesInQuotes: false
			};

			var settings = $.extend( {}, defaults, options );

			return this.each( function() {
				create( $( this ), settings );

				if ( typeof settings.expand !== 'undefined' ) {
					$( this ).jsonPresenter( 'expand', settings.expand );
				}
			} );
		} else if ( arguments[ 0 ] === 'destroy' ) {
			return this.each( function() {
				destroy( $( this ) );
			} );
		} else if ( arguments[ 0 ] === 'expandAll' ) {
			return this.each( function() {
				expandAll( getRootNode( $( this ) ) );
			} );
		} else if ( arguments[ 0 ] === 'collapseAll' ) {
			return this.each( function() {
				collapseAll( getRootNode( $( this ) ) );
			} );
		} else if ( arguments[ 0 ] === 'expand' ) {
			var depth = arguments[ 1 ];
			return this.each( function() {
				collapseAll( getRootNode( $( this ) ) );
				expand( getRootNode( $( this ) ), depth );
			} );
		}
	};
} )( jQuery );
